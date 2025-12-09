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
