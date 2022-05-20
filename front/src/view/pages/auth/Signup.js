/* Register.js */
import React,{useState} from "react"
import axios from "axios";
import { useNavigate,Link } from 'react-router-dom';
import classes from './../../../style/page/Signup.module.css'

const Signup= (props) => {

  const [name,setName]=useState("")
  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")
  //const [passwordConfirmation, setPasswordConfirmation] = useState("")

  const navigate=useNavigate()

  //APIに送信
  const handleSubmit =(event)=>{ 
    console.log(email)
    console.log(name)
    console.log(password)
    axios.post("http://localhost:5001/signup",
    {
      user:{
        email:email,
        name:name,
        password:password,
      }
    },
    // { withCredentials: true } //cookieを含むか
    ).then(res=>{ //ユーザー作成成功
        props.setToken(res.data.data.token)
        console.log(res.data.data)
        if (res.data.code===1){
          console.log("ログイン成功しました")
          console.log(res.data.data.token)
          navigate('/home')
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
        <p className={classes.titleStyle}>メールアドレス</p>
        <input 
          type="email" 
          name="email" 
          value={email} 
          onChange={event=> setEmail(event.target.value)}
          className={classes.inputStyle}
        />
        <br />
        <p className={classes.titleStyle}>ユーザー名</p>
        <input 
          type="name" 
          name="name"
          value={name}
          onChange={event=> setName(event.target.value)}
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
        <button type="submit" className={classes.submitButtonStyle} onClick={handleSubmit}> <Link to="/home" className={classes.linkStyle}>登録</Link></button>
      </form>

      <button className={classes.backButtonStyle}> <Link to="/" className={classes.linkStyle}>戻る</Link></button>
    </>
  );
};

export default Signup;