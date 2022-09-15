import { Link } from 'react-router-dom';
import classes from './../../style/page/Top.module.css'

const Top = (props) => {
  
  return (
    <>
    <div className={classes.box}>
      <div className={classes.backgroundStyle1}></div>
      <div className={classes.backgroundStyle2}></div>
      <div className={classes.containerStyle}>
         <img className={classes.logoStyle} src={`${process.env.PUBLIC_URL}/img/logo.png`} alt="ロゴ"/>
        {/* <h2>ログイン状態: {props.loggedInStatus}</h2>
        <Registration handleSuccessfulAuthentication={handleSuccessfulAuthentication}/>
        <Login handleSuccessfulAuthentication={handleSuccessfulAuthentication}/>
        <button onClick={handleLogoutClick}>ログアウト</button> */}
        <br />
        <button className={classes.buttonStyle}> <Link  className={classes.linkStyle} to="/signup">新規登録</Link></button>
        <br />
        <button className={classes.buttonStyle}> <Link to="/signin" className={classes.linkStyle}>ログイン</Link></button>
      </div>
      <div className={classes.container}>
       <div className={classes.backgroundStyle3}></div>
       <div className={classes.backgroundStyle4}></div> 
      </div>
      </div>
    </>
  );
};

export default Top;