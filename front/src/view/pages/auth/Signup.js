/* Register.js */
import React,{useState} from "react"
import axios from "axios";
import { Link } from 'react-router-dom';
import classes from './../../../style/Signup.module.css'

const Signup= (props) => {

  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")
  const [passwordConfirmation, setPasswordConfirmation] = useState("")

  //APIに送信
  const handleSubmit =(event)=>{ 
    console.log(email)
    console.log(password)
    axios.post("http://localhost:5000/signup",
    {
      user:{
        email:email,
        password:password,
        password_confirmation: passwordConfirmation
      }
    },
    { withCredentials: true } //cookieを含むか
    ).then(res=>{ //ユーザー作成成功
        console.log("registration res", res)
        if(res.data.status==='create'){ //railsのAPIのdata.statasを見て判断する。
          props.handleSuccessfullAuthentication(res.data) //新規登録画面に飛ぶ(home.jsの関数)
        }
        
       
    }).catch(err=>{//ユーザー作成失敗
        console.log("registration res", err)
    })
    event.preventDefault()
  }
  
  return (
    <>
      
      <form className={classes.formStyle} onSubmit={handleSubmit} >
        <h1 className={classes.helloStyle}>ようこそ</h1>
        <p className={classes.titleStyle}>ユーザー名</p>
        <input 
          type="email" 
          name="email" 
          value={email} 
          onChange={event=> setEmail(event.target.value)}
          className={classes.inputStyle}
        />
        <br />
        <p className={classes.titleStyle}>パスワード</p>
        <input 
          type="password"
          name="password" 
          value={password}
          onChange={event=> setPassword(event.target.value)}
          className={classes.inputStyle}
        />
        <br />
        <p className={classes.titleStyle}>確認用パスワード</p>
        <input 
          type="password" 
          name="password_confirmation" 
          value={passwordConfirmation}
          onChange={event=> setPasswordConfirmation(event.target.value)}
          className={classes.inputStyle}
        />
        <br />
        <button type="submit" className={classes.submitButtonStyle}><Link to="/home" className={classes.linkStyle}>登録</Link></button>
      </form>

      <button className={classes.backButtonStyle}> <Link to="/" className={classes.linkStyle}>戻る</Link></button>
    </>
  );
};

export default Signup;