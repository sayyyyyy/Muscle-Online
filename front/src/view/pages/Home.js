import Footer from "../components/Footer";
import classes from "./../../style/page/Home.module.css"
import Modal from "./../components/Modal"
import { useState } from "react";
const Home=()=>{

  const [showModal, setShowModal]=useState(false);

  const openModal=()=>{
    setShowModal(true);
  }

  return(
    <>
      <h1>ホーム画面</h1>
      <button className={classes.button} onClick={openModal}>
       <img src={`${process.env.PUBLIC_URL}/img/roombattle1.png`} alt="ルームボタン" className={classes.roomimg} />
      </button>
      <Modal showFlag={showModal} setShowModal={setShowModal}/>


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