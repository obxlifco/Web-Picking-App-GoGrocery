import { Component, OnInit,Inject, ViewChild} from '@angular/core';
import { GlobalService } from '../global/service/app.global.service';
import {  Router } from '@angular/router';
import { NgForm } from '@angular/forms';


@Component({
    selector: 'app-contactus',
    templateUrl: './contactus.component.html',
    styleUrls: ['./contactus.component.css']
})
export class ContactusComponent implements OnInit {
    userdata: any;
    name='';
    email='';
    number:number;
    message=''
    
    @ViewChild('contactForm') contactForm: any;

    constructor(
        private globalservice:GlobalService, private router:Router

    ) { 
        this.userdata=JSON.parse(localStorage.getItem('currentUser'));
        
    }

    ngOnInit() {
        window.scroll(0,0);
    }
    doFormSubmit(form: NgForm){
     
        let data={
            name:form.value.FullName,
            email:form.value.Email,
            phone:form.value.PhoneNumber.toString(),
            message:form.value.Message,
        }
        this.globalservice.contactus(data).subscribe(res=>{
            this.globalservice.showToast('Query Submitted successfully');
            form.resetForm();
        },
        err=>{
            this.globalservice.showToast('Something went wrong');
        })

    }

}