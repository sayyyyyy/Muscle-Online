import Footer from "../components/Footer";
import classes from "./../../style/page/Home.module.css"
const Home=()=>{
  return(
    <>
      <h1>ホーム画面</h1>
      <button className={classes.button}>
       <img src={`${process.env.PUBLIC_URL}/img/roombattle1.png`} alt="ルームボタン" className={classes.roomimg} />
      </button>

      <button className={classes.ratebutton}>
       <img src={`${process.env.PUBLIC_URL}/img/rate.png`} alt="ルームボタン" className={classes.rateimg} />
      </button>

      

      <div>

      </div>
      <Footer />
    </>
  )

}

export default Home;