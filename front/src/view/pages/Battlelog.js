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
            <div className={classes.backgroundStyle1}></div>
            <div className={classes.totalResult}>
                <div className={classes.ResultBox}>
                    <p className={classes.totalResultText}>Win</p>
                    {/* <h1 className={classes.totalResultNum}>{userlog.win}</h1> */}
                    <h1 className={classes.totalResultNum}>0</h1>
                </div>
                <div></div>
                <div className={classes.ResultBox}>
                    <p className={classes.totalResultText}>Lose</p>
                    {/* <h1 className={classes.totalResultNum}>{userlog.lose}</h1> */}
                    <h1 className={classes.totalResultNum}>1</h1>
                </div>
            </div>

            <div className={classes.totalBattlelog}>
                <div>　</div>
               <div className={classes.battlelog}>
                   <h2 className={classes.battleResult}>Win</h2>
                   <h4 className={classes.battleUserName}>いわぐちやすひろ</h4>
                   <h3 className={classes.battleTimes}>43<span>回</span></h3>
               </div>
               <div className={classes.battlelog}>
                   <h2 className={classes.battleResult}>Win</h2>
                   <h4 className={classes.battleUserName}>いわぐちやすひろ</h4>
                   <h3 className={classes.battleTimes}>43<span>回</span></h3>
               </div>
            </div>            
            <Footer />
        </>
    )
}

export default Battlelog;
