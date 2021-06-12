import { Component, OnInit,Inject, ViewChild} from '@angular/core';
import { GlobalService } from '../global/service/app.global.service';
import {  Router } from '@angular/router';
import { NgForm } from '@angular/forms';


@Component({
    selector: 'app-promotion',
    templateUrl: './promotion.component.html',
    styleUrls: ['./promotion.component.css']
})
export class PromotionComponent implements OnInit {
    userdata: any;
    name='';
    email='';
    number:number;
    message=''

    constructor(
        private globalservice:GlobalService, private router:Router

    ) { 
        this.userdata=JSON.parse(localStorage.getItem('currentUser'));
        
    }

    ngOnInit() {
        window.scroll(0,0);
    }
    
}