import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProducttaxComponent } from './producttax.component';

describe('ProducttaxComponent', () => {
  let component: ProducttaxComponent;
  let fixture: ComponentFixture<ProducttaxComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProducttaxComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProducttaxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
