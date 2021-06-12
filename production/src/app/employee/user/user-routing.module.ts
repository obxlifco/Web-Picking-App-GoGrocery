import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UserComponent }  from '../../employee/user/employee.user.component';
import { UserAddEditComponent }  from '../../employee/user/employee.user.addedit.component'; 


const routes: Routes = [
  {
    path:'',
    component:UserComponent
  },
  {
    path:'add',
    component:UserAddEditComponent
  },
  {
    path:'edit/:id',
    component:UserAddEditComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
