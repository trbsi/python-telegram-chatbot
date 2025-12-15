if (isUnlocked ?? false) {
    // -------------------- VIDEO PLAYER -----------------------
    const player = videojs('my-video', {
        controlBar: {
            fullscreenToggle: false,
            pictureInPictureToggle: false
        }
    });

    // Resize player to fit viewable screen
    player.ready(function() {
        player.on('loadedmetadata', function() {
            resizeVideo();
        });
    });

    // Re-run on window resize
    window.addEventListener('resize', resizeVideo);

    // Start feeding shard
    const mediaSource = new MediaSource();
    const videoUrl = URL.createObjectURL(mediaSource);

    // Set up VideoJS with MediaSource
    player.src({
        src: videoUrl,
        type: videoMetadata.codec // Important for MSE
    });


    mediaSource.addEventListener("sourceopen", async () => {
        const sourceBuffer = mediaSource.addSourceBuffer(videoMetadata.codec);

        const queue = [];
        let ended = false;
        let appending = false; // tracks if appendNext is currently processing

        async function fetchShards() {
            const videoMasterKey = await decryptKeys();
            const shards = maskAndOrder();

            for (const shard of shards) {
                const shardBytes = await fetchAndDecryptShard(shard, videoMasterKey);
                queue.push(shardBytes);
                // Try appending immediately if SourceBuffer is free
                appendNext();
            }

            ended = true; // signal all shards have been queued
            appendNext(); // in case queue is empty but ended
        }

        function appendNext() {
            // Prevent re-entrant calls
            if (appending) return;
            appending = true;

            while (!sourceBuffer.updating && queue.length > 0) {
                const shard = queue.shift();
                try {
                    sourceBuffer.appendBuffer(shard);
                    console.log("Appending shard, queue length:", queue.length);
                    // Wait for 'updateend' before next append
                    break;
                } catch (err) {
                    console.error("Failed to append shard:", err);
                    // Push back the shard and retry later
                    queue.unshift(shard);
                    break;
                }
            }

            // End MediaSource if all shards appended
            if (!sourceBuffer.updating && queue.length === 0 && ended) {
                try {
                    mediaSource.endOfStream();
                    console.log("All shards appended, MediaSource ended");
                } catch (err) {
                    console.error("Failed to end MediaSource:", err);
                }
            }

            appending = false;
        }

        // Listen for 'updateend' to append the next shard
        sourceBuffer.addEventListener("updateend", appendNext);

        // Start fetching and queuing shards
        fetchShards();
    });


    /**
     * Resize the Video.js player to fit the viewport height while
     * maintaining the video's original aspect ratio.
     * If the resulting width exceeds the viewport width, scale down
     * proportionally to fit within the screen width.
     */
    function resizeVideo() {
        const header = $('header');
        const windowWidth = window.innerWidth - 30; // optional padding
        const windowHeight = window.innerHeight - header.height() - 20; // minus header

        // Get intrinsic video dimensions
        const videoWidth = player.videoWidth();
        const videoHeight = player.videoHeight();

        if (!videoWidth || !videoHeight) return; // metadata not loaded yet

        const videoAspect = videoWidth / videoHeight;

        let newHeight = windowHeight;           // fit height to screen
        let newWidth = newHeight * videoAspect; // adjust width to keep aspect ratio

        // If width exceeds screen, scale down
        if (newWidth > windowWidth) {
            newWidth = windowWidth;
            newHeight = newWidth / videoAspect; // adjust height to keep aspect ratio
        }

        // Apply new size to Video.js player
        player.width(newWidth);
        player.height(newHeight);

        // Center horizontally
        player.el().style.margin = '0 auto';
    }

    function hexToBytes(hex) {
        const bytes = new Uint8Array(hex.length / 2);
        for (let i = 0; i < hex.length; i += 2) {
            bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
        }
        return bytes;
    }

    async function decryptKeys() {
        const sessionKeyBytes = hexToBytes(sessionKey);
        const wrappedMasterKeyBytes = hexToBytes(videoKey);
        const wrapNonceBytes = hexToBytes(videoNonce);

        // Import session key as AES-GCM key
        const cryptoKey = await crypto.subtle.importKey(
            "raw",
            sessionKeyBytes,
            "AES-GCM",
            false,
            ["decrypt"]
        );

        // Decrypt the wrapped master key
        const masterKeyBytes = await crypto.subtle.decrypt({
                name: "AES-GCM",
                iv: wrapNonceBytes
            },
            cryptoKey,
            wrappedMasterKeyBytes
        );

        // Import master key to decrypt shards
        const masterKey = await crypto.subtle.importKey(
            "raw",
            masterKeyBytes,
            "AES-GCM",
            false,
            ["decrypt"]
        );

        return masterKey;
    }

    async function fetchAndDecryptShard(shardMeta, videoMasterKey) {
        // 1. Fetch encrypted shard
        const response = await fetch(shardMeta.url);
        const encryptedBytes = new Uint8Array(await response.arrayBuffer());

        // 2. Convert nonce
        const nonceBytes = hexToBytes(shardMeta.nonce);

        // 3. Decrypt shard with master key
        const decryptedBytesBuffer = await crypto.subtle.decrypt({
                name: "AES-GCM",
                iv: nonceBytes
            },
            videoMasterKey,
            encryptedBytes
        );

        const decryptedBytes = new Uint8Array(decryptedBytesBuffer);

        // 4. Reverse scramble / XOR
        const unscrambled = decryptedBytes.map(byte => {
            // Step 1: Rotate bits left
            const rotated = ((byte >> 3) | (byte << 5)) & 0xFF;

            // Step 2: XOR with the mask from shardMeta
            const result = rotated ^ shardMeta.mask;

            // Step 3: Return the result
            return result;
        });

        //     saveUnscrambledShard(unscrambled, shardMeta.name + '.mp4')
        return unscrambled;
    }

    function saveUnscrambledShard(arrayBuffer, fileName = "shard.mp4") {
        // Convert ArrayBuffer to Blob
        const blob = new Blob([arrayBuffer], {
            type: "video/mp4"
        });

        // Create a temporary link
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = fileName;

        // Trigger download
        document.body.appendChild(link); // required for Firefox
        link.click();

        // Cleanup
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
    }

    function maskAndOrder() {
        shards = []
        videoMetadata.shards.forEach((shard) => {
            name = shard['name'];
            split_name = name.split('_')

            index = split_name[1].slice(4)
            mask = split_name[2].slice(4)

            shard['mask'] = mask // mask is integer number
            shards[index] = shard
        });

        return shards;
    }



    // ------------------------------ TESTING ---------------------------------
    async function initializeSimplePlayerAndTest(videoMetadata) {
        const video = videojs('my-video');

        try {
            // const shards = maskAndOrder(videoMetadata);
            // const videoMasterKey = await decryptKeys();
            // const firstShardBytes = await fetchAndDecryptShard(shards[0], videoMasterKey);
            codec = 'video/mp4; codecs="avc1.4D401F, mp4a.40.2"';
            codec = 'video/webm; codecs="vp9, opus"';
            codec = 'video/webm; codecs="vp8, vorbis"';
            const mediaSource = new MediaSource();
            const source = URL.createObjectURL(mediaSource);
            video.src({
                src: source,
                type: codec
            });

            shardUrl = 'https://protectapp.loc/static/output.webm';
            if (MediaSource.isTypeSupported(codec)) {
                console.log('Codec supported ✅');
            } else {
                console.log('Codec NOT supported ❌');
            }
            mediaSource.addEventListener('sourceopen', async () => {
                const sourceBuffer = mediaSource.addSourceBuffer(codec);

                // Always attach listener BEFORE appendBuffer
                sourceBuffer.addEventListener('updateend', () => {
                    if (!sourceBuffer.updating && mediaSource.readyState === 'open') {
                        mediaSource.endOfStream();
                        video.play();
                    }
                });

                // Fetch shard
                const arrayBuffer = await fetch(shardUrl).then(r => r.arrayBuffer());

                // Optional: unscramble here
                // arrayBuffer = unscramble(arrayBuffer);

                sourceBuffer.appendBuffer(arrayBuffer);
            });

        } catch (e) {
            console.error("Initialization error:", e);
            video.src = "";
        }
    }
    //initializeSimplePlayerAndTest(videoMetadata);
}
