import { Component, OnInit,ViewChild } from '@angular/core';
import { from } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Router, NavigationEnd } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { NotificationserviceService } from 'src/app/notificationservice.service';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  @ViewChild('drawer') sidenav: MatSidenav | any;

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
  close(){
    this.sidenav.close()
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
