import { Link } from 'react-router-dom';

const StartBattle=()=>{
    return (
        <>
            <h1>対戦準備画面</h1>
            <Link to="/battle">準備完了</Link>
        </>
    )
}

export default StartBattle;