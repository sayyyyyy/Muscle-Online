import { Link } from 'react-router-dom';
import classes from "./../../style/page/FinishBattle.module.css"

const FinishBattle=()=>{
    return (
        <>
            <div className={classes.b}> 
                <div className={classes.resultContainer}>
                    <h1>Winner</h1>
                    <h1>63<span>回</span></h1>
                    <hr/>
                    <h1>Looser</h1>
                    <h1>32<span>回</span></h1>
                </div>
                <button className={classes.backButtonStyle}> <Link to="/home" className={classes.linkStyle}>戻る</Link></button>      
            </div>
        </>
    )
}

export default FinishBattle;