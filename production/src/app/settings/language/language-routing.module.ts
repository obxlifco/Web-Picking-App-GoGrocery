import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LanguageComponent } from './settings.language.component';

const routes: Routes = [
    { path: '', component: LanguageComponent },
    { path: 'reload', component: LanguageComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LanguageRoutingModule { }
