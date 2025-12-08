function singleMediaComponent(
    mediaId,
    totalLikes,
    totalComments,
    isLiked,
    likeMediaApi,
    createCommentApi,
    listCommentsApi,
    reportContentApi
) {
    return {
        liked: isLiked,
        likeCount: totalLikes,
        commentsCount: totalComments,
        commentsOpen: false,
        comments: [],
        commentsLoading: false,
        commentInput: '',
        showReportForm: false,
        reportDescription: '',

        init() {
            this.openComments();
        },

        async like() {
            // Animate the icon
            const icon = event.currentTarget.querySelector('i');
            icon.classList.add('scale-125');
            setTimeout(() => icon.classList.remove('scale-125'), 150);

            // Optimistic UI
            const previousLiked = this.liked;
            const previousLikes = this.likeCount;
            this.liked = !this.liked;
            this.likeCount += this.liked ? 1 : -1;

            try {
                tempLikeMediaApi = likeMediaApi.replace('__MEDIA_ID__', mediaId)
                const res = await fetch(tempLikeMediaApi, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    credentials: 'include'
                });
                if (!res.ok) throw new Error('Like failed');
                // optionally update counts from server response
                const data = await res.json();
                if (data.like_count != null) this.likeCount = data.like_count;
            } catch (e) {
                // rollback
                this.liked = previousLiked;
                this.likeCount = previousLikes;
                console.error(e);
                alert('Failed to update like. Try again.');
            }
        },

        async submitComment() {
            const text = this.commentInput.trim();
            if (!text) return;

            // optimistic add
            const temp = {
                id: 'temp-' + Date.now(),
                text,
                user: {
                    username: 'You',
                    avatar: '/path/to/avatar.png'
                },
                created_at: 'just now'
            };
            this.comments.unshift(temp);
            this.commentInput = '';
            // increment comments_count in UI
            this.commentsCount = (this.commentsCount || 0) + 1;

            var body = {
                'media_id': mediaId,
                'comment': text
            }

            try {
                const res = await fetch(createCommentApi, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(body)
                });
                if (!res.ok) throw new Error('Failed to post comment');
                const saved = await res.json();
                // replace temp comment with saved comment (if server returns it)
                // naive approach: replace first temp id
                const idx = this.comments.findIndex(comment => comment.id === temp.id);
                if (idx !== -1 && saved) {
                    this.comments.splice(idx, 1, saved);
                }
            } catch (e) {
                // rollback UI changes
                this.comments = this.comments.filter(comment => comment.id !== temp.id);
                this.commentsCount = Math.max(0, (this.commentsCount || 1) - 1);
                console.error(e);
            }
        },

        async openComments() {
            this.commentsOpen = true;
            this.comments = [];
            this.commentInput = '';
            this.commentsLoading = true;

            try {
                tempListCommentsApi = listCommentsApi.replace('__MEDIA_ID__', mediaId)
                const res = await fetch(tempListCommentsApi);
                if (!res.ok) throw new Error('Failed to fetch comments');
                const data = await res.json();
                this.comments = data.results || data;
            } catch (e) {
                console.error(e);
                alert('Failed to load comments.');
            } finally {
                this.commentsLoading = false;
            }
        },

        openReportForm() {
            this.showReportForm = true;
        },

        closeReportForm() {
            this.showReportForm = false;
            this.reportDescription = '';
        },

        async submitReport() {
            try {
                const res = await fetch(reportContentApi, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: JSON.stringify({
                        type: 'media',
                        content_id: mediaId,
                        description: this.reportDescription
                    }),
                    credentials: 'include'
                });

                if (!res.ok) throw new Error('Report failed');
                await res.json();

                alert('Thanks for your feedback. We’ll review this content shortly.');
                this.showReportForm = false;
                this.reportDescription = "";
            } catch (e) {
                console.error(e);
            }
        },
    }
}

// ----------- VIDEO DECRYPTING ---------------
function resizeVideo() {
    const video = document.getElementById('my-video');
    const windowWidth = window.innerWidth - 40;
    const windowHeight = window.innerHeight;

    // Get video original aspect ratio
    const videoAspect = video.videoWidth / video.videoHeight;
    const windowAspect = windowWidth / windowHeight;

    if (videoAspect > windowAspect) {
        // Video is wider than viewport → fit width
        video.style.width = windowWidth + 'px';
        video.style.height = (windowWidth / videoAspect) + 'px';
    } else {
        // Video is taller than viewport → fit height
        video.style.height = windowHeight + 'px';
        video.style.width = (windowHeight * videoAspect) + 'px';
    }
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
    console.log(shardMeta)

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


// -------------------- VIDEO PLAYER -----------------------
const player = videojs('my-video');

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