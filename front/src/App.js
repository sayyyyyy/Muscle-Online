import { BrowserRouter, Routes, Route } from "react-router-dom";
import {useState,useEffect} from "react"
import axios from "axios";

import Top from "./view/pages/Top";
import Registration from "./view/pages/auth/Registration";
import Login from "./view/pages/auth/Login";
import Home from "./view/pages/Home";

const App = (props) => {

  const [loggedInStatus,setLoggedInStatus]=useState("未ログイン") //ユーザーのログイン状態を参照
  const [user, setUser] = useState({})//ユーザーをログインさせる際に必要

  const handleLogin=(data)=>{
    setLoggedInStatus("現在ログインしております") //ログインして or いないの文章をここで変換
    setUser(data.user)//userオブジェクトの値を書き換えています。
  }

  const handleLogout=(data)=>{
    setLoggedInStatus("未ログイン")
    setUser({})

  }
  useEffect(()=>{//ページがリロードされるたびに毎回呼び出される
    checkLoginStatus()
  })

  const checkLoginStatus=()=>{
    axios.get("http://localhost:5000/logged_in",{withCredentials: true})//logged_inはアクション名　ここを変更すれば良い
    .then(res => {
      console.log("ログイン状況", res)
    }).catch(err => {
      console.log("ログインエラー", err)
    })
  }
  return (
    <BrowserRouter>
      <Routes>
        <Route path={`/`} element={<Top {...props}  handleLogin={handleLogin}  handleLogout={handleLogout} loggedInStatus={loggedInStatus}/>} />
        {/* <Route path={`/dashboard/`} element={<Dashboard {...props} loggedInStatus={loggedInStatus} />} /> */}
        <Route path={`/registration`} element={<Registration {...props}  handleLogin={handleLogin}  handleLogout={handleLogout} loggedInStatus={loggedInStatus}/>}/>
        <Route path={`/login`} element={<Login {...props}  handleLogin={handleLogin}  handleLogout={handleLogout} loggedInStatus={loggedInStatus}/>}/>
        <Route path={`/home`}  render={props =>( <Home {...props}  handleLogin={handleLogin}  handleLogout={handleLogout} loggedInStatus={loggedInStatus}/>)} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;