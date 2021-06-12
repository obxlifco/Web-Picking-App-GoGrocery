import { Component, OnInit,Inject, ViewChild} from '@angular/core';
import { GlobalService } from '../global/service/app.global.service';
import {  Router } from '@angular/router';
import { NgForm } from '@angular/forms';


@Component({
    selector: 'app-contactus',
    templateUrl: './mobilelanding.component.html',  
})
export class MobileLandingComponent implements OnInit {
    userdata: any;
    
    constructor(
        private globalservice:GlobalService, private router:Router

    ) { 
        this.userdata=JSON.parse(localStorage.getItem('currentUser'))       
    }

    ngOnInit() {
       this.checkMobile();
    }



        checkMobile() {

            var os = this.getMobileOperatingSystem();

            console.log(os)

            if (os !== "unknown") {

                if (os === "Android") {

                    setTimeout(function () {

                        window.location.href = "https://play.google.com/store/apps/details?id=com.gogrocery&hl=en"

                    }, 500);

                }

                else if (os === "IOS") {

                    setTimeout(function () {

                        window.location.href = "https://apps.apple.com/us/app/gogrocery/id1503352361";

                    }, 500);

                }

               

            } else {

                    setTimeout(function () {

                        window.location.href = "https://www.gogrocery.ae";

                    }, 500);

            }

        }

 

        getMobileOperatingSystem() {

            var userAgent = navigator.userAgent || navigator.vendor;

 

            // Windows Phone must come first because its UA also contains "Android"

            if (/windows phone/i.test(userAgent)) {

                return "Windows Phone";

            }

 

            if (/android/i.test(userAgent)) {

                return "Android";

            }

 

            // iOS detection

            //if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
             if (/iPad|iPhone|iPod/.test(userAgent)) {

                return "IOS";

            }

 

            return "unknown";

        }
   

}