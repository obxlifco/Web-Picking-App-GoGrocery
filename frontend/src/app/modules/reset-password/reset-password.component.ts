import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../../global/service/authentication.service';
import { LoginComponent } from '../../login/login.component';
import { GlobalService } from '../../global/service/app.global.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
@Component({
  selector: 'app-res-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent implements OnInit {
  model: any = {};
  msg:'';
  constructor( 
    private _route: ActivatedRoute,
    private router:Router,
    private _authService:AuthenticationService,
    private _gs:GlobalService,
    public dialog: MatDialog) {
  }

  ngOnInit() {
    
  }

  loginComponent: MatDialogRef<LoginComponent> | null;
  onSubmit(){
    this._gs.showLoaderSpinner(true);
    let id='';
    id = this._route.snapshot.paramMap.get('id');
    let data={
      "new_password":this.model.newpassword,
      "confirm_password":this.model.confirmPassword,
      "pin_code":id 
    }
    
    this._authService.confirmPassword(data).subscribe(res=>{
      this._gs.showLoaderSpinner(false);
      if(res['status'] == 1) {
        // setTimeout(() => {
            this.loginComponent = this.dialog.open(LoginComponent, {
              disableClose: true
            });
            this.loginComponent.afterClosed().subscribe(response => {
              this.router.navigate(['/']);
            })
        // }, 100);
      }
      this.msg=res['message'];
    },
    error => {
      this.msg = error['message'] ? error['message'] : 'Something went wrong';
      this._gs.showLoaderSpinner(false);


    }
    )
  }
}