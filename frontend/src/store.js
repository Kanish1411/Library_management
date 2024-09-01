import { createStore } from "vuex";

const store=createStore({
    state(){
        return{
            token: localStorage.getItem('token'),
            login:false,
            lib:false,
            admin:false,
        }
    },
    mutations:{
        setlogin(state,payload){
            state.login=payload;
        },
        setlib(state,payload){
            state.lib=payload;
        },
        setadmin(state,payload){
            state.admin=payload;
        },
    }
})
export default store;