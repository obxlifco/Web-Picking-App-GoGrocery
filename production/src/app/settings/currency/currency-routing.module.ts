import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CurrencyComponent } from './settings.currency.component';

const routes: Routes = [
	{ path: '', component: CurrencyComponent },
    { path: 'reload', component: CurrencyComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CurrencyRoutingModule { }
