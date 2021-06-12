import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FailedorderComponent } from './failedorder.component';

describe('FailedorderComponent', () => {
  let component: FailedorderComponent;
  let fixture: ComponentFixture<FailedorderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FailedorderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FailedorderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
