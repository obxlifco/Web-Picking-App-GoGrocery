import { Component, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { MatDialogRef, MatDialog } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginComponent } from '../login/login.component';
import { AuthenticationService } from '../global/service/authentication.service';
import { GlobalService } from '../global/service/app.global.service';

@Component({
  selector: 'app-forget-password',
  templateUrl: './forget-password.component.html',
  styleUrls: ['./forget-password.component.css']
})
export class ForgetPasswordComponent implements OnInit {
  forgetForm: FormGroup;
  // loading = false;
  // submitted = false;
  returnUrl: string;
  msg = '';
  model: any = {};
  isError:Boolean=false;
  
  public hide: string = 'password';
  constructor(
      private dialogRef: MatDialogRef<ForgetPasswordComponent>,
      private route: ActivatedRoute,
      private router: Router,
      private authenticationService:AuthenticationService,
      public dialog:MatDialog,
      private _globalService:GlobalService
  ) { }

  ngOnInit() {

     
  }
  

  onSubmit(){
    this._globalService.showLoaderSpinner(true);
    this.authenticationService.forgetPassword(this.model.email).subscribe(res=>{
      
      if(res && res['status'] == 1) {
         if(res['success_message']){
            
            this.msg="Hi"+" "+res['name']+" "+"kindly check your mail";
          }else{
              this.msg= res['name'];
          }
       } else {
         this.msg = res['message'];
       }
       this._globalService.showLoaderSpinner(false);
    },
    error => {
      this._globalService.showLoaderSpinner(false);
      this.msg = "Something went wrong,please try again";
    }
    )
  }
 

  // check_login() {
  //     this.authenticationService.login(this.model.email, this.model.password)
  //         .subscribe(
  //             data => {

  //                 if(data && data['status'] == 200){
  //                     // this.router.navigate([this.returnUrl]);
  //                     this.dialogRef.close();
  //                 }else{
  //                    this.isError=true;
  //                    this.error="Invalid Email Or Password"
  //                 }
                  
  //             },
  //             error => {
  //                 this.error = error;
  //                 // this.loading = false;
  //             });
  // }
 
  closeDialog() {
      this.dialogRef.close();
  }
  
 onSignIn() {
      this.dialogRef.close('sign-in');
      //this.openSignupDialog();
  }
  
  /* openSignupDialog() {
       let signupPopupRef = this.dialog.open(SignUpComponent,{
           disableClose:true

       });
       signupPopupRef.afterClosed().subscribe(response => {
          if(response == 'sign-in') {
              alert("hiii");

          }

       });

   }*/


}