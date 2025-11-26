function adultPopup(balanceEndpoint) {
    return {
        open: false,

        showPopup() {
            if (this.getLocalStorage() != 1) {
                this.open = true;
            }
        },

        continueToSite() {
            this.setLocalStorage();
            this.open = false
        },

        exit() {
            window.location.href = "https://www.bing.com";
        },

        getLocalStorage() {
            return localStorage.getItem("18_plus_consent");
        },

        setLocalStorage() {
            return localStorage.setItem("18_plus_consent", 1);
        }
    }
}