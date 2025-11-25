import { Router } from "express";
import {register_controller, login_Controller , logOutUser  , refreshAccessToken} from "../controllers/auth.controller.js";
import { verifyJWT } from "../middlware/auth.js";



const router = Router();

router.route('/register').post(register_controller);


router.route('/login').post(login_Controller);  

router.route('/logout').post ( verifyJWT , logOutUser)    
router.route('/refresh-Token').post (refreshAccessToken)    



export default router; 