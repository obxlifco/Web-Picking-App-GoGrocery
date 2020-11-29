import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddproductasSubtituteComponent } from './addproductas-subtitute.component';

describe('AddproductasSubtituteComponent', () => {
  let component: AddproductasSubtituteComponent;
  let fixture: ComponentFixture<AddproductasSubtituteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddproductasSubtituteComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddproductasSubtituteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
