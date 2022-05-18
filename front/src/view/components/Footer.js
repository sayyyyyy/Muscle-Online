import { Link } from 'react-router-dom';
import classes from "./../../style/components/Footer.module.css"
import { BsClipboardData } from "react-icons/bs"
import { AiOutlineHome } from "react-icons/ai";
import { AiOutlineUser } from "react-icons/ai";

const Footer=(props)=>{
   return(
    <footer className={classes.footerStyle}>
      <Link to="/battlelog" className={classes.linkStyle}><BsClipboardData className={classes.iconStyle}/></Link>
      <Link to="/home" className={classes.linkStyle}><AiOutlineHome className={classes.iconStyle}/></Link>
      <Link to="/mypage" className={classes.linkStyle}><AiOutlineUser className={classes.iconStyle} /></Link>
    </footer>
   )
}

export default Footer;