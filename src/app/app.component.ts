import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Router, NavigationEnd } from '@angular/router';
import { ApiService } from './services/api/api.service';
import { DatabaseService } from './services/database/database.service';
import { GlobalitemService } from './services/globalitem/globalitem.service';
import { ModalService } from './services/modal/modal.service';
import { ForgotpasswordComponent } from './user/login/forgotpassword/forgotpassword.component';
import { NotificationserviceService } from './notificationservice.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'lifco Picking pp';
  loginRouterLink: any
  totalbadge:any=0
  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );
    isLoggedIn$: Observable<boolean> | any;   

  constructor(private breakpointObserver: BreakpointObserver,
    private router: Router,
    private apiService: ApiService,
    public globalitems: GlobalitemService,
    private db: DatabaseService,
    private notificationservice : NotificationserviceService
  ) {
    console.log("router link : ", this.loginRouterLink);
    router.events.subscribe((url: any) =>
      this.getURL(url.url)
    );

    this.initializeMethod()
  }

  initializeMethod() {
    this.isuerlogin()
  }
  getURL(url?: any) {
    this.loginRouterLink = url?.url
    console.log("router link : ", this.loginRouterLink);
  }
  ngOnInit(): void {
    this.isLoggedIn$ = this.db.isLoggedIn(); 
    this.initializedTimer()
  }

  initializedTimer(){
    this.notificationservice.startcounter()
  }

  isuerlogin() {
    this.apiService.getIPAddress().subscribe(data => {
      console.log("Ip Address : ", data);
      this.db.setIP(data)
    })
  }
  logout() {

    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);
      this.db.getIP().then(data1 => {
        data1.api

        let data = {
          ip_address: data1.ip,
          device_id: data1.ip,
        }

        this.apiService.postData("picker-logout/", data).subscribe((data: any) => {
          console.log("logout : ", data);
          if (data.status === 1) {
            this.globalitems.showSuccess("You have Sucessfully logout", "Success")
            this.db.SignOut();
            this.router.navigate(["login"])
          }

        })
      })

    })
  }
  setbadge(badge:any){
    this.totalbadge=badge
  }
  navigatLatestOrder(){
    this.totalbadge=0;
    this.router.navigate(['orders'])
  }

  

}
