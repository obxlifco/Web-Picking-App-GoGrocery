import {
    Component, OnInit, Inject, Optional
}
from '@angular/core';
import {
    MatDialogRef, MatDialog, MAT_DIALOG_DATA
}
from '@angular/material';
import {
    Router
}
from '@angular/router';
import {
    LanguageService
}
from './settings.language.service';
import {
    GlobalService
}
from '../../global/service/app.global.service';
@
Component({
    templateUrl: './templates/manage_language.html',
    providers: [LanguageService]
})
export class LanguageManageComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public language_list: any;
    public formModel: any = {};
    public base_language: any = [];
    public rate: any = [];
    public post_data: any = [];
    private sub: any;
    constructor(
        private _languageService: LanguageService,
        private _globalService: GlobalService,
        private _router: Router,
        private dialogRef: MatDialogRef < LanguageManageComponent > ,
        public dialog: MatDialog, @Optional()@ Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
            let containerElem: HTMLElement = < HTMLElement > document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
    }
    ngOnInit() {
        let that = this;
        this._languageService.languageLoad(0).subscribe(
            data => {
                this.response = data;
                this.language_list = this.response.api_status;
                this.language_list.forEach(function(item: any) {
                    if (item.isbaselanguage == 'y') {
                        that.base_language = item;
                    }
                    that.rate[item.id] = item.exchange_rate;
                });
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }
    sync() {
        let base_lang = this.base_language.language_code;
        let that = this;
        this._languageService.syncLang(this._globalService.getUserId()).subscribe(
            data => {
                this.response = data;
                this.language_list = this.response.AllLanguages;
                this.language_list.forEach(function(item: any) {
                    if (item.isbaselanguage == 'y') {
                        that.base_language = item;
                    }
                    that.rate[item.id] = item.exchange_rate;
                });
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }
    manageLanguage(form: any) {
        this.errorMsg = '';
        let that = this;
        let data: any = {};
        this.language_list.forEach(function(item: any) {
            let language: any = {};
            language.id = item.id;
            language.engageboost_company_website_id = 1;
            language.engageboost_language_master_id = item.engageboost_language_master_id;
            language.language_code = item.language_code;
            language.exchange_rate = that.rate[item.id];
            language.isbaselanguage = item.isbaselanguage;
            language.country_id = item.country_id;
            language.createdby = that._globalService.getUserId();
            language.updatedby = that._globalService.getUserId();
            that.post_data.push(language);
        });
        data = {
            data: that.post_data
        };
        this._languageService.languageManage(data).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    this.closeDialog();
                } else {
                    this.errorMsg = this.response.message;
                }
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }
    closeDialog() {
        this.dialogRef.close();
    }
}

@Component({
    templateUrl: './templates/add_language.html',
    providers: [LanguageService]
  })
  export class LanguageAddEditComponent implements OnInit { 
      public response: any;
      public errorMsg: string;
      public successMsg: string;
      public formModel: any = {};
      public ipaddress: any;
      public all_languages:any = [];
      constructor(
          private _languageService:LanguageService,
          private _globalService:GlobalService,
          private _router: Router,
          private dialogRef: MatDialogRef<LanguageAddEditComponent>,
          public dialog: MatDialog,
          @Optional() @Inject(MAT_DIALOG_DATA) public data: any
      ) {
          dialog.afterOpen.subscribe(() => {
             let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
             containerElem.classList.remove('pop-box-up');
          });
          this.ipaddress = _globalService.getCookie('ipaddress'); 
      }
      
      ngOnInit(){
          this.formModel.languageId = this.data;
          if(this.formModel.languageId>0){
              this._languageService.languageLoad(this.formModel.languageId).subscribe(
                     data => {
                      this.response = data;
                      this.all_languages = data.all_languages;
                         if(this.formModel.languageId>0){
                          this.formModel = Object.assign({}, this.response.api_status);
                             this.formModel.languageId = this.response.api_status.id;
                          this.formModel.lamguageName = this.response.api_status.name;
                          this.formModel.status = this.response.api_status.isblocked; 
                         }else{
                             this.formModel.languageId = 0;
                         }
                     },
                     err => console.log(err),
                     function(){
                         //completed callback
                     }
              );
          } else {
              this._languageService.languageLoad(0).subscribe(
                  data => {
                      this.response = data;
                      if (this.response.status>0){
                          this.all_languages = data.all_languages;
                      }
                  },
                  err => console.log(err),
                  function(){
                      //completed callback
                  }
               );
          }
      }
  
      addEditLanguage(form: any){
          this.errorMsg = '';
          var data: any = {};
          data.website_id = this._globalService.getWebsiteId();
          data.name = this.formModel.languageName;
          Object.keys(this.formModel).forEach(key => {
              let res = key;
              let value = this.formModel[key];
              if (res != this.formModel.languageName && res != this.formModel.status) {
                  data[res]=value;
              }
              data.isblocked = this.formModel.status;
          });
  
          if(this.formModel.languageId<1){
                data.createdby = this._globalService.getUserId();
          }
          data.updatedby = this._globalService.getUserId();
          if(this.ipaddress) {
              data.ip_address=this.ipaddress;
          } else {
              data.ip_address='';
          }
          this._languageService.languageAddEdit(data,this.formModel.languageId).subscribe(
                 data => {
                     this.response = data;
                    if(this.response.status==1){
                     this.closeDialog();
                     //this._router.navigate(['/brand/reload']);
                  }else {
                     this.errorMsg = this.response.message;
                     }
              },
                 err => console.log(err),
                 function(){
                  //completed callback
                 }
          );
      }
  
      closeDialog(){
          this.dialogRef.close();
      }
  }