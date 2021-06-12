import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TaxsettingsComponent } from './taxsettings.component';

const routes: Routes = [
  {  
    path: '', component:TaxsettingsComponent 
  },    
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaxsettingsRoutingModule { }