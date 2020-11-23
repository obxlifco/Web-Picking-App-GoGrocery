import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddproductcategoryComponent } from './addproductcategory.component';

describe('AddproductcategoryComponent', () => {
  let component: AddproductcategoryComponent;
  let fixture: ComponentFixture<AddproductcategoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddproductcategoryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddproductcategoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
