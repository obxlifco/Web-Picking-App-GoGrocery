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

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  // { path: '', component: DashboardComponent },
  {
    path: 'dashboard', component: DashboardComponent,

    // children: [
    //  { path: 'orders', component: OrdersComponent},
    //   { path: 'returns', component: ReturnsComponent},
    //   { path: 'stocks', component: StocksComponent},
    //   { path: 'home', component: HomeComponent},
    // ]
  },
  { path: 'orders', component: OrdersComponent },
  { path: 'returns', component: ReturnsComponent },
  { path: 'stocks', component: StocksComponent },
  { path: 'home', component: HomeComponent },

  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
