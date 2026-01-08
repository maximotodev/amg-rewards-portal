import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface Receipt {
  id?: number;
  user_id: string;
  merchant_name: string;
  total_amount: number;
  purchase_date: string;
  status?: string;
  points_earned?: number;
}

@Injectable({
  providedIn: 'root',
})
export class ReceiptService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/receipts';

  // Using a Signal to manage state (Senior Angular pattern)
  receipts = signal<Receipt[]>([]);

  fetchReceipts(): void {
    this.http.get<Receipt[]>(this.apiUrl).subscribe((data) => {
      this.receipts.set(data);
    });
  }

  submitReceipt(receipt: Receipt): Observable<Receipt> {
    return this.http.post<Receipt>(this.apiUrl, receipt).pipe(
      tap(() => this.fetchReceipts()) // Refresh list after submission
    );
  }
}
