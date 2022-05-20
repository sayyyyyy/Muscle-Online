import { BrowserRouter, Routes, Route } from "react-router-dom";
import {useState,useEffect} from "react"
import axios from "axios";

import useToken from './view/components/useToken'

import Top from "./view/pages/Top";
import Signup from "./view/pages/auth/Signup";
import Signin from "./view/pages/auth/Signin";
import Home from "./view/pages/Home";
import Battlelog from "./view/pages/Battlelog"
import Mypage from "./view/pages/Mypage"
import Loading from "./view/pages/Loading"



const App = () => {
  const { token, removeToken, setToken } = useToken();
  
  return (
    <BrowserRouter>
      <Routes>
        <Route path={`/`} element={<Top />} />
        <Route path={`/signup`} element={<Signup setToken={setToken}/>}/>
        <Route path={`/signin`} element={<Signin setToken={setToken}/>}/>
     {/* トークンがない場合 */}
        {!token && token!=="" &&token!== undefined?  
        <Route path={`/signin`} element={<Signin setToken={setToken}/>}/>
        :(
          <>
              <Route path={`/home`}  element={ <Home  token={token} />}/>
              <Route path={`/battlelog`}  element={ <Battlelog token={token} /> }/>
              <Route path={`/mypage`}  element={ <Mypage token={token}  />} />
              <Route path={`/loading`}  element={ <Loading token={token}  />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  );
};

export default App;