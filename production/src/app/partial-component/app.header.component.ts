import { Component,ElementRef,OnInit } from '@angular/core';
import { Http } from '@angular/http';
import { HeaderService } from './app.header.service';
import { Router } from '@angular/router';
import { GlobalService } from '../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { MatDialog,MatDialogRef } from '@angular/material';
import { AccountDetailsComponent,PasswordUpdateComponent } from '../profile/app.profile.component';


@Component({
  selector: '<header-menu></header-menu>',
  templateUrl: './templates/header.html',
  providers: [HeaderService],
  host: {
    '(document:click)': 'onClick($event)',
  },
})
export class HeaderComponent implements OnInit { 
  public response : any;
	public errorMsg: string;
	public successMsg: string;
	public global_search:any=[];
  public user_first_name: string;
  public is_superadmin:string;
  public website_list : any;
  public selectedItem =0;
	constructor(
    private _headerService: HeaderService,
    private _router: Router,
    private elRef:ElementRef,
    private globalService: GlobalService,
    private _cookieService:CookieService,
    public dialog: MatDialog,
    private http: Http
  ) {
      globalService.profileNameChange$.subscribe(
        (value) => {
          this.user_first_name = value;
        }
      );    
      
      globalService.websitelist$.subscribe(
        (value) => {
          if(value == true){
            var data: any = {};
            data.company_id = 1;   
            this.getwebsitelist(data);
          }       
        }
      );   
  }
  

  onClick(event: any) {
   if (!this.elRef.nativeElement.contains(event.target)) // or some similar check
    this.close_search_div();
  }

  ngOnInit(){    
    let userData = this._cookieService.getObject('userData');    
    if(userData){
      this.user_first_name = userData['first_name'];
      this.is_superadmin = userData['isSuperAdmin'];         
    }      
    var data: any = {};
    data.company_id = 1;   
    this.getwebsitelist(data);
    this.selectedItem = this.globalService.getWebsiteId();    
  }
  getwebsitelist(data:any){   
    this._headerService.getwebsiteList(data).subscribe(
      data => {
        if(data.status==1)
          this.website_list = data.api_status;
        else
          this.website_list = [];  
      }
    );    
  }
  get_websitedetails(website_id : number){ 
    let userData = this._cookieService.getObject('userData');  
    userData['website_id'] = website_id;
    if(website_id){
      this._cookieService.putObject('userData', userData);
      this.selectedItem = this.globalService.getWebsiteId();
      this.globalService.onChangeWebsite();
    }
    this._router.navigate(['/dashboard']);
  }
  globalSearch(txt:string){
		//this._headerService.doSearch(txt).subscribe(
    this._headerService.doSearchDirect(txt).subscribe(
        data => {
       		this.response = data;
       		this.global_search = this.response.hits.hits;
       		if(this.global_search.length>0){
       			this.elRef.nativeElement.querySelector('.dropdownsearch').style.display="block";
       		}else{
       			this.errorMsg = this.response.message;
       		}	
        },
        err => console.log(err),
        function(){}
    );
  }
  
  close_search_div(){
    this.elRef.nativeElement.querySelector('.dropdownsearch').style.display="none";
    this.elRef.nativeElement.querySelector('#search').value="";
  }
  
  logout() {
    // this.globalService.showLoaderSpinner(true);
    this.globalService.navLinks = [
        { id: 1, label: 'Dashboard', url: 'dashboard', parent: 0 }
    ];
    this._cookieService.remove('userData');
    this._cookieService.remove('tabs');
    this._cookieService.removeAll();
    this._router.navigate(['/']);  
  }

  changeClass() {
    if(document.querySelector('.maincontainer').classList.contains('full')){
        document.querySelector('.maincontainer').classList.remove('full');
    } else {
        document.querySelector('.maincontainer').classList.add('full');
    }

    // if (document.querySelector('.innertab_sec').classList.contains('full_intab')) {
    //   document.querySelector('.innertab_sec').classList.remove('full_intab');
    // } else {
    //   document.querySelector('.innertab_sec').classList.add('full_intab');
    // }

    if (document.querySelector('.bottom_fixedpart').classList.contains('back_expand')) {
      document.querySelector('.bottom_fixedpart').classList.remove('back_expand');
    } else {
      document.querySelector('.bottom_fixedpart').classList.add('back_expand');
    }
  }

  dialogRef1: MatDialogRef<AccountDetailsComponent> | null;
  openDetailsPop() {
    this.dialogRef1 = this.dialog.open(AccountDetailsComponent);
  }

  dialogRef2: MatDialogRef<PasswordUpdateComponent> | null;
  openPasswordPop() {
    this.dialogRef2 = this.dialog.open(PasswordUpdateComponent);
  }

  toggleFullScreen() {
    var document:any = window.document;  
    var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
            (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
            (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
            (document.msFullscreenElement && document.msFullscreenElement !== null);
    var docElm = document.documentElement;
    if (!isInFullScreen) {
        if (docElm.requestFullscreen) {
            docElm.requestFullscreen();
        } else if (docElm.mozRequestFullScreen) {
            docElm.mozRequestFullScreen();
        } else if (docElm.webkitRequestFullScreen) {
            docElm.webkitRequestFullScreen();
        } else if (docElm.msRequestFullscreen) {
            docElm.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
  }
}
