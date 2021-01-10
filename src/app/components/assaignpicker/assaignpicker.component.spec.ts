import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssaignpickerComponent } from './assaignpicker.component';

describe('AssaignpickerComponent', () => {
  let component: AssaignpickerComponent;
  let fixture: ComponentFixture<AssaignpickerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AssaignpickerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssaignpickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
