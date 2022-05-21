import { Link } from 'react-router-dom';
import classes from "./../../style/page/StartBattle.module.css"

const StartBattle=()=>{
    return (
        <>
            <div classes={classes.background}>
                <h1>対戦準備画面</h1>
                <button className={classes.readyButton}><Link to="/battle" className={classes.linkStyle}>準備完了</Link></button>
            </div>
        </>
    )
}

export default StartBattle;