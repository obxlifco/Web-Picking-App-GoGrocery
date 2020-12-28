import { DataSource } from '@angular/cdk/collections';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ModalService } from 'src/app/services/modal/modal.service';
import { ForgotpasswordComponent } from './forgotpassword/forgotpassword.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  @ViewChild('showpasswordvalue', { static: true }) showpasswordValue: ElementRef | any;
  loginForm: any = FormGroup;
  loading = false;
  submitted = false;
  returnUrl: any;
  error = '';
  useripAddress: any;

  constructor(
    private formBuilder: FormBuilder,
    private globalitem: GlobalitemService,
    public apiservice: ApiService,
    public router: Router,
    public modalservice : ModalService,
    private database: DatabaseService
    // private authenticationService: AuthenticationService
  ) {

    // redirect to home if already logged in
    if (this.database.isLoggedIn()) {
      this.router.navigate(['dashboard/home']);
    }
    
  }
  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      device_id: ['']
    });
    this.getIp()
  }

  // convenience getter for easy access to form fields
  get f() { return this.loginForm.controls; }

  login() {
    this.submitted = true;
    // stop here if form is invalid
    if (this.loginForm.invalid) {
      return;
    }
    // console.log("login form data : ", this.loginForm.value);
    
    // this.globalitem.showSpinner()
    this.apiservice.postData("picker-login/", this.loginForm.value).subscribe((res: any[]) => {
      console.log(res);
      let data:any=res;
      if(data.status === 0){
        this.globalitem.showError(data.message, "Error")
        console.log("form value : ",);
      }else{
        // this.globalitem.showSuccess("You have Successfully login", "Success")
        console.log("form value : ",this.loginForm.username);
        if(this.loginForm.value.username === "supermgr"){
          let warehouseids={
            warehouse_id:null
          }
          Object.assign(data?.user_data,warehouseids)
        }
        this.database.setUserData(data?.user_data)
        this.router.navigate(["dashboard/home"])
      }
      
    })
    // .catch(error => {
    //   this.globalitem.hideSpinner()
    //   this.globalitem.showError(error.message,"Error")
    // })
  }
  navigateproduct() {
    setTimeout(() => {
      this.router.navigate(['products']);
      console.log("inside login");

    }, 1500);
  }

  getIp() {
    this.database.getIP().then(data => {
      this.loginForm.controls['device_id'].setValue(data.ip);
    })
  }

  forrgotePassword(){
    this.modalservice.openModal('',ForgotpasswordComponent )
  }

  showpassword(event:any){
    console.log("event Value : ",event);
    if (event.checked) {
      this.showpasswordValue.nativeElement.setAttribute('type', 'text');
      // span.innerHTML = 'hide';
    } else {
      this.showpasswordValue.nativeElement.setAttribute('type', 'password');
      // span.innerHTML = 'show';
    }
  }
}
