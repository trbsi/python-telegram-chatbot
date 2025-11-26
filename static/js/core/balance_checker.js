function balanceChecker(balanceEndpoint, isAuthenticated) {
    return {
        balance: null,
        open: false,
        pollingInterval: null,
        pollingRate: 1 * 60 * 1000, // 1 minute
        storage_key: 'balance_checker',

        async balancePolling() {
            if (!isAuthenticated) {
                return
            }
            await this.fetchBalance();
            this.startPolling();
        },

        async fetchBalance() {
            console.log('Balance checked');
            if (this.getWithExpiry() !== null) {
                return;
            }

            try {
                const res = await fetch(balanceEndpoint);
                const data = await res.json();
                this.balance = data.balance;

                if (data.status === 'low_balance') {
                    this.open = true;
                } else if (data.status === 'hide') {
                    this.stopPolling();
                }

            } catch (err) {
                console.error('Balance check failed:', err);
            }
        },

        startPolling() {
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
            }

            // Start a new one with the current pollingRate
            this.pollingInterval = setInterval(() => {
                this.fetchBalance();
            }, this.pollingRate);
        },

        stopPolling() {
            clearInterval(this.pollingInterval);
        },

        closePopup() {
            this.open = false;
            this.setWithExpiry();
            this.startPolling();
        },

        setWithExpiry() {
            const now = Date.now();
            const item = {
                value: true,
                expiry: now + 10 * 60 * 1000, //10 minutes
            };
            localStorage.setItem(this.storage_key, JSON.stringify(item));
        },

        getWithExpiry() {
            const itemStr = localStorage.getItem(this.storage_key);
            if (!itemStr) return null;

            const item = JSON.parse(itemStr);
            const now = Date.now();

            if (now > item.expiry) {
                localStorage.removeItem(this.storage_key);
                return null;
            }

            return item.value;
        }
    }
}

async function canSpend(type) {
    try {
        const response = await fetch('/payment/api/can-spend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({type: type})
            }
        );

        const json = await response.json()
        if (!response.ok) {
            throw json;
        }

        let oldBalance = parseFloat(json.balance)
        const intervalId = setInterval(async () => {
            const response = await fetch('/payment/api/balance');
            const json = await response.json();
            const newBalance = parseFloat(json.balance);
            if (newBalance != oldBalance) {
                showBalanceNotification(oldBalance, newBalance);
                clearInterval(intervalId);
            }
        }, 2000);

        return {'ok': true}

    } catch (exception) {
        toastr.warning(exception.error);
        return {'ok': false, 'error': exception.error}
    }
}

function showBalanceNotification(oldBalance, newBalance) {
    const notification = $("#balance-notification");

    // Calculate change
    const isNegative = (newBalance < oldBalance);
    const change = newBalance - oldBalance;

    // Prepare starting text
    notification.text(`${oldBalance} coins`);

    // Show the div
    notification.removeClass("hidden");

    // Animate number from old → new
    let start = oldBalance;
    const end = newBalance;
    const duration = 500; // 1 seconds
    const startTime = performance.now();

    function animateBalance(timestamp) {
        const progress = Math.min((timestamp - startTime) / duration, 1);
        const current = Math.floor(start + (end - start) * progress).toFixed(2);
        notification.text(`${current} coins`);

        if (progress < 1) {
            requestAnimationFrame(animateBalance);
        } else {
            // show final text with delta for clarity
            notification.text(`${newBalance} coins (${change})`);
        }
    }

    requestAnimationFrame(animateBalance);

    // Hide after animation duration (5s total)
    setTimeout(() => {
        notification.addClass("hidden");
    }, 3000);
}