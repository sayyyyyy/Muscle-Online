import Login from './auth/Login'
import Registration from './auth/Registration'
import axios from 'axios';
import { Link } from 'react-router-dom';


const Top = (props) => {
  const handleSuccessfulAuthentication=(data)=>{ //dataとはユーザーオブジェクト
        props.handleLogin(data) //App.jsより
        props.history.push("/dashboard")// /dashboardへ画面遷移させる処理
  }

  const handleLogoutClick=()=>{//ログアウト
     axios.delete("http://localhost:5000/logout", { withCredentials: true })
            .then(res => {
                props.handleLogout()
            }).catch(error => console.log("ログアウトエラー", error))
    }

    

  return (
    <>
       <h1>スタート画面</h1>
      {/* <h2>ログイン状態: {props.loggedInStatus}</h2>
      <Registration handleSuccessfulAuthentication={handleSuccessfulAuthentication}/>
      <Login handleSuccessfulAuthentication={handleSuccessfulAuthentication}/>
      <button onClick={handleLogoutClick}>ログアウト</button> */}
     
      <button> <Link to="/registration">新規登録</Link></button>
      <button> <Link to="/login">ログイン</Link></button>

    </>
  );
};

export default Top;