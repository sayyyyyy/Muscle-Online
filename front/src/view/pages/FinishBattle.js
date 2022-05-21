import { Link } from 'react-router-dom';
import classes from "./../../style/page/FinishBattle.module.css"

const FinishBattle=()=>{
    return (
        <>
            <div className={classes.resultBackground}> 
                <button className={classes.backButtonStyle}> <Link to="/home" className={classes.linkStyle}>戻る</Link></button>  
                <div className={classes.resultContainer}>
                    <h1>win</h1>
                    <h2>岩口</h2>
                    <h1>63<span>回</span></h1>
                    <hr/>
                    <h1>lose</h1>
                    <h2>ぐちお</h2>
                     <h1>40<span>回</span></h1>
                </div>    
            </div>
        </>
    )
}

export default FinishBattle;