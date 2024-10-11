import axios from 'axios';

export async function checkLogin(store, router) {
    const tk = localStorage.getItem("token");
    if (!tk) {
        store.commit("setlogin", false);
        alert("Login to access this page");
        router.push("/");
        return false;
    }
    try {
        const resp = await axios.get("/checkLogin", {
            headers: {
                Authorization: "Bearer " + tk,
            },
        });
        if (resp.data.msg === "Valid") {
            store.commit("setlogin", true);
            return true;
        } else {
            store.commit("setlogin", false);
            alert("Login Required");
            router.push("/");
            return false;
        }
    } catch (error) {
        alert("There was an error: " + error);
        router.push("/");
        return false;
    }
}

export async function checkLib(store, router) {
    const tk = localStorage.getItem("token");
    if (!tk) {
        store.commit("setlib", false);
        alert("Login to access this page");
        router.push("/");
        return false;
    }
    try {
        const resp = await axios.get("/checkLib", {
            headers: {
                Authorization: "Bearer " + tk,
            },
        });
        if (resp.data.msg === "Valid") {
            store.commit("setlib", true);
            return true;
        } else {
            store.commit("setlib", false);
            alert("Only Librarian Allowed");
            router.push("/");
            return false;
        }
    } catch (error) {
        alert("There was an error: " + error);
        router.push("/");
        return false;
    }
}

export async function checkAd(store, router) {
    const tk = localStorage.getItem("token");
    if (!tk) {
        store.commit("setadmin", false);
        alert("Login to access this page");
        router.push("/");
        return false;
    }
    try {
        const resp = await axios.get("/checkAd", {
            headers: {
                Authorization: "Bearer " + tk,
            },
        });
        if (resp.data.msg === "Valid") {
            store.commit("setadmin", true);
            return true;
        } else {
            store.commit("setadmin", false);
            alert("Only Admins Allowed");
            router.push("/");
            return false;
        }
    } catch (error) {
        alert("There was an error: " + error);
        router.push("/");
        return false;
    }
}