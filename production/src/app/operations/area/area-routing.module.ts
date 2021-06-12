import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AreaAddEditComponent } from './area.addedit.component';
import { AreaComponent } from './area.component';
const routes: Routes = [
  {
    path:'',component:AreaComponent
  },
  {
    path:'add',component:AreaAddEditComponent
  },
  {
    path:'edit/:id',component:AreaAddEditComponent
  },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AreaRoutingModule { }
