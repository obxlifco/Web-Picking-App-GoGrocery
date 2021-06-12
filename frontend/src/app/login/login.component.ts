import { Component, OnInit,Inject} from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../global/service/authentication.service';
import { GlobalService } from '../global/service/app.global.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { SignUpComponent } from '../modules/sign-up/sign-up.component';
import { ForgetPasswordComponent } from '../forget-password/forget-password.component';
import { AuthService } from "angularx-social-login";
import { FacebookLoginProvider, GoogleLoginProvider } from "angularx-social-login";
import { CookieService } from 'ngx-cookie';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
    loginForm: FormGroup;
    // loading = false;
    // submitted = false;
    returnUrl: string;
    error = '';
    model: any = {};
    isError: Boolean = false;
    isChecked: Boolean = false;

    public hide: string = 'password';
    constructor(
        private dialogRef: MatDialogRef<LoginComponent>,
        @Inject(MAT_DIALOG_DATA) public actionData:any,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        public dialog: MatDialog,
        private authService: AuthService,
        private _cookieService:CookieService,
        private _gs:GlobalService
    ) { }

    ngOnInit() {
      
        let isValue = localStorage.getItem('isChecked') == 'true' ? true : false;
        let clientIp = this._cookieService.get('client_ip') ? this._cookieService.get('client_ip') : '';
        if (isValue) {
            this.isChecked = isValue;
            this.model.email = JSON.parse(localStorage.getItem('userData')).email;
            this.model.password = JSON.parse(localStorage.getItem('userData')).password;
        }
       
        // this.authenticationService.logout();

        // get return url from route parameters or default to '/'
        // this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }
    socialLogin(socialType) {
       if(socialType == 'google') {
           this.authService.signIn(GoogleLoginProvider.PROVIDER_ID);
       } else if(socialType == 'facebook') {
           this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
       }
    }

    showPassword() {
        if (this.hide == 'password') {
            this.hide = 'text';
        } else {
            this.hide = 'password';
        }
    }



    check_login() {
        localStorage.setItem('isChecked', this.isChecked.toString());
        this._gs.showLoaderSpinner(true);
        this.authenticationService.login(this.model.email, this.model.password)
            .subscribe(
                data => {
                    this._gs.showLoaderSpinner(false);
                    if (data && data['status'] == 200) {
                        // this.router.navigate([this.returnUrl]);
                        this.dialogRef.close();
                        let credential = {
                            "email": this.model.email,
                            "password": this.model.password
                        }
                        localStorage.setItem('userData', JSON.stringify(credential));
                        if(Object.keys(this.actionData).length > 0 && this.actionData['redirectUrl']) {
                            this.router.navigate([this.actionData['redirectUrl']]);
                        } 

                    } else {
                        this._gs.showLoaderSpinner(false);
                        this.isError = true;
                        this.error = "Invalid Email Or Password"
                    }

                },
                error => {
                    this._gs.showLoaderSpinner(false);
                    this.error = error;
                    // this.loading = false;
                });
    }
    /**
     * Method for closing dialog
     * @access public
    */
    closeDialog() {
        this.dialogRef.close();
    }
    /**
     * Method for poping up sign up form
     * @access public
    */
    onSignUpRequest() {
        this.dialogRef.close('sign-up');
        //this.openSignupDialog();
    }
    forgetpassword() {
        this.dialogRef.close('forget-password');
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