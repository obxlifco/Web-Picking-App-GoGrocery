import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NowarehousefoundComponent } from './nowarehousefound.component';

describe('NowarehousefoundComponent', () => {
  let component: NowarehousefoundComponent;
  let fixture: ComponentFixture<NowarehousefoundComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NowarehousefoundComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NowarehousefoundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
