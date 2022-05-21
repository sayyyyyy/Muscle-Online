import Footer from "../components/Footer"
import { useEffect,useState} from "react"
import axios from "axios"
import classes from "./../../style/page/Battlelog.module.css"

const Battlelog=(props)=>{

    const [userlog,setUserlog]=useState([])

    useEffect(()=>{
        const gethistory=async()=>{
            const res =await axios.post("http://localhost:5001/history",
            {
                user_token:props.token,
            }
            ).then(res=>{
                if (res.data.code===1){
                    console.log("対戦ログを取得しました")
                    setUserlog(res.data.data.user_data)
                    console.log(res.data.data.user_data)
                }
                else{
                    console.log(res.data.data.states)
                }
            }
            ).catch(res=>{
                console.log(2)
            }
            )
        }
        gethistory()
    }, [])

    return(
        <>
            
            <div className={classes.totalResult}>
                <div>
                    <p className={classes.t}>Win</p>
                    <h1 className={classes.totalResultWinNum}>{userlog.win}</h1>
                    <h1 className={classes.totalResultWinNum}>1</h1>
                </div>
                <div>
                    <p>Lose</p>
                    <h1>{userlog.lose}</h1>
                    <h1 className={classes.totalResultWinNum}>0</h1>
                </div>
            </div>
            
            <Footer />
        </>
    )
}

export default Battlelog;
