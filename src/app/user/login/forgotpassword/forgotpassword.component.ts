import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';

@Component({
  selector: 'app-forgotpassword',
  templateUrl: './forgotpassword.component.html',
  styleUrls: ['./forgotpassword.component.scss']
})
export class ForgotpasswordComponent implements OnInit {

  email:any
  forrgotform:any= FormGroup;
  submitted=false
  constructor(public apiService: ApiService,public globalitems : GlobalitemService,
    public dialogRef: MatDialogRef<ForgotpasswordComponent>,
    private formBuilder: FormBuilder,
    ) { }

  ngOnInit(): void {
    this.forrgotform = this.formBuilder.group({
      useremail: ['', Validators.required],
    });
  
  }

  forgotpassword() {

    this.submitted = true;
    // stop here if form is invalid
    if (this.forrgotform.invalid) {
      return;
    }

    let data = {
      email:this.email,
    }
      this.apiService.postData("picker-forgot-password/", data).subscribe((data: any) => {
        console.log("latestorders : ", data);
        if(data.status === 1){
          this.globalitems.showSuccess(data.message,"Sent")
          this.dialogRef.close()
        }
      })
  }
  get f() { return this.forrgotform.controls; }

  closeModal() {
    this.dialogRef.close()
  }
  
}
