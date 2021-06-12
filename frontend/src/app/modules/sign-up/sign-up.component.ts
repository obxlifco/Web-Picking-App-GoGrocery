import { Component, OnInit,Inject} from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { AuthenticationService } from '../../global/service/authentication.service';
import { GlobalService } from '../../global/service/app.global.service';
import {GlobalVariable} from '../../global/service/global';
import {LoginComponent} from '../login/login.component';
import { FacebookLoginProvider, GoogleLoginProvider } from "angularx-social-login";
import { AuthService } from "angularx-social-login";


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

    signUpForm: FormGroup;
    submitted:boolean = false;
    returnUrl: string;
    error = '';
    model: any = {};
    isError:Boolean=false;
    carrierCode = GlobalVariable.CARRIER_CODE;
    selectedCarrierCode;
    countryCode = GlobalVariable.COUNTRY_CODE;

    
    public hide: string = 'password';

    constructor(
    	private dialogRef: MatDialogRef<SignUpComponent>,
    	@Inject(MAT_DIALOG_DATA) public actionData:any,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private _gs:GlobalService,
        private _dialog:MatDialog,
        private authService : AuthService,

    ) {
    	
     }

	ngOnInit() {


	}
	/**
	 * Method for signing up
	 * @access public
	*/
	signup() {
		this._gs.showLoaderSpinner(true);
		let signupData = this.model;
		//signupData['phone'] = (GlobalVariable.COUNTRY_CODE+signupData['carrier_code'].toString()+signupData['phone'].toString()).trim();
		this.authenticationService.signup(signupData).subscribe(response => {
			this._gs.showLoaderSpinner(false);
			if(response && response['status'] == 200) {
				this._gs.showToast("You have successfully signed up");
				if(Object.keys(this.actionData).length > 0 && this.actionData['redirectUrl']) {
                    this.router.navigate([this.actionData['redirectUrl']]);
                 } 
				this.dialogRef.close();
				 

			}

		},
		error => {
			console.log("************** Error ***************");
			console.log(error);
			this._gs.showLoaderSpinner(false);
			let errorMessage = error && error['error_message'] ? error['error_message'] : 'Something went wrong,Please try again';
			this.isError = true;
			this.error = errorMessage;
			/*this._gs.showToast(errorMessage);*/
		}
		);
	}
	 socialLogin(socialType) {
       if(socialType == 'google') {
           this.authService.signIn(GoogleLoginProvider.PROVIDER_ID);
       } else if(socialType == 'facebook') {
           this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
       }
    }
	showPassword(){
        if(this.hide=='password'){
			this.hide = 'text';
		} else {
			this.hide = 'password';
		}
    }
	/**
	 * Method on closing dialog
	 * @access publuic
	*/
	closeDialog() {
		this.dialogRef.close();
	}
	
	
	openSignInPopup() {
		this.dialogRef.close('sign-in');
		
		
	 }

}
