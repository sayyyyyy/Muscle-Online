import {useState} from "react"

const useToken=()=>{
    //ローカルストレージからトークンの取得
    const getToken=()=>{
        const userToken=localStorage.getItem('token');
        return userToken && userToken //トークンが存在する場合にのみトークンを返す
    }
    
    const [token,setToken]=useState(getToken())

    //トークンを保存する
    const saveToken=(userToken)=>{
        localStorage.setItem('token',userToken)
        setToken(userToken);
    }

    //トークンの削除
    const removeToken=()=>{
        localStorage.removeItem("token")
        setToken(null);
    }
    
    return {
    setToken: saveToken,
    token,
    removeToken
  }

}

export default useToken;