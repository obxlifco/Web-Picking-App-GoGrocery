import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HomeComponent } from './dashboard/pages/home/home.component';
import { OrdersComponent } from './dashboard/pages/orders/orders.component';
import { ReturnsComponent } from './dashboard/pages/returns/returns.component';
import { StocksComponent } from './dashboard/pages/stocks/stocks.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { TestComponent } from './test/test.component';
import { LoginComponent } from './user/login/login.component';
import { AppsettingsComponent } from './components/appsettings/appsettings.component';
import { dashCaseToCamelCase } from '@angular/compiler/src/util';
import { SalesreportComponent } from './dashboard/pages/salesreport/salesreport.component';
import { AuthguardGuard } from './services/authguard/authguard.guard';
import { NotfoundComponent } from './components/notfound/notfound.component';

// const routes: Routes = [
//   { path: 'login', component: LoginComponent },
//   { path: '', redirectTo: '/login', pathMatch: 'full' },
//   // { path: '', component: DashboardComponent },
//   {
//     path: 'dashboard', component: DashboardComponent,
//   },
//   { path: 'orders', component: OrdersComponent },
//   { path: 'returns', component: ReturnsComponent },
//   { path: 'stocks', component: StocksComponent },
//   { path: 'home', component: HomeComponent },
//   { path: 'appsettings', component: AppsettingsComponent },


// ];

const appRoutes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  {
    path: 'dashboard', component: DashboardComponent,
    children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' ,canActivate: [AuthguardGuard]},
      { path: 'home', component: HomeComponent ,canActivate: [AuthguardGuard] },
      { path: 'orders', component: OrdersComponent ,canActivate: [AuthguardGuard]},
      { path: 'returns', component: ReturnsComponent,canActivate: [AuthguardGuard] },
      { path: 'stocks', component: StocksComponent ,canActivate: [AuthguardGuard]},
      { path: 'salesreport', component: SalesreportComponent,canActivate: [AuthguardGuard] },
      { path: 'appsettings', component: AppsettingsComponent ,canActivate: [AuthguardGuard]},
    ]
  },
  {path: '404', component: NotfoundComponent},
  {path: '**', redirectTo: '/404'}
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
