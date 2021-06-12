import { TestBed } from '@angular/core/testing';

import { LoyaltypointService } from './loyaltypoint.service';

describe('LoyaltypointService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: LoyaltypointService = TestBed.get(LoyaltypointService);
    expect(service).toBeTruthy();
  });
});
