/* Register.js */
import React,{useState} from "react"
import axios from "axios";
import { useNavigate,Link } from 'react-router-dom';
import classes from './../../../style/page/Signin.module.css'

const Signin= (props) => {

  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")
  
  const navigate=useNavigate()

  //APIに送信
  const handleSubmit =(event)=>{ 
    axios.post("http://localhost:5001/signin",
    {
      user:{
        email:email,
        password:password,
      }
    }
    ).then(res=>{ //ユーザー作成成功
        props.setToken(res.data.data.token)//josnからtoken取得
        if (res.data.code===1){
          console.log("ログイン成功しました")
          console.log(res.data.data.token)
          navigate('/home')
        }
    }).catch(err=>{//ユーザー作成失敗
        console.log("registration res", err)
        console.log(err.response)
        console.log(err.response.status)
        console.log(err.response.headers)
    })
    setEmail("")
    setPassword("")
    event.preventDefault()
    
  }
  
  return (
    <>
      <div className={classes.backgroundStyle1}></div>
      <div className={classes.backgroundStyle2}></div>

      <form onSubmit={handleSubmit} className={classes.formStyle}>
        <h1 className={classes.helloStyle}>おかえりなさい</h1>
        <p className={classes.titleStyle}>メールアドレス</p>
        <input 
          type="email" 
          name="email" 
          placeholder="メールアドレス" 
          value={email} 
          onChange={event=> setEmail(event.target.value)}
          className={classes.inputStyle}
        />
        <br />
        <p className={classes.titleStyle}>パスワード</p>
        <input 
          type="password"
          name="password" 
          placeholder="パスワード"
          value={password}
          onChange={event=> setPassword(event.target.value)}
          className={classes.inputStyle}
        />
        <button type="submit" onClick={handleSubmit} className={classes.submitButtonStyle} > <Link to="/home" className={classes.linkStyle}>登録</Link></button>
      </form>
      <button className={classes.backButtonStyle}> <Link to="/" className={classes.linkStyle}>戻る</Link></button>
      <div className={classes.backgroundStyle3}></div>
      <div className={classes.backgroundStyle4}></div>
    </>
  );
};

export default Signin;