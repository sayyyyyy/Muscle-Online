import Login from './auth/Signin'
import Registration from './auth/Signup'
import axios from 'axios';
import { Link } from 'react-router-dom';
import classes from './../../style/page/Top.module.css'

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
      <div className={classes.backgroundStyle1}></div>
      <div className={classes.backgroundStyle2}></div>
      <div className={classes.containerStyle}>
         <img className={classes.logoStyle} src={`${process.env.PUBLIC_URL}/img/logo.png`} alt="ロゴ"/>
        {/* <h2>ログイン状態: {props.loggedInStatus}</h2>
        <Registration handleSuccessfulAuthentication={handleSuccessfulAuthentication}/>
        <Login handleSuccessfulAuthentication={handleSuccessfulAuthentication}/>
        <button onClick={handleLogoutClick}>ログアウト</button> */}
        <br />
        <button className={classes.buttonStyle}> <Link  className={classes.linkStyle} to="/registration">新規登録</Link></button>
        <br />
        <button className={classes.buttonStyle}> <Link to="/login" className={classes.linkStyle}>ログイン</Link></button>
      </div>
      {/* <div className={classes.backgroundStyle3}></div>
      <div className={classes.backgroundStyle4}></div> */}
    </>
  );
};

export default Top;