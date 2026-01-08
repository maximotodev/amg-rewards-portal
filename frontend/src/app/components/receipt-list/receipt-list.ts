import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReceiptService } from '../../services/receipt';

@Component({
  selector: 'amg-receipt-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="list-container">
      <h3>Recent Submissions</h3>
      <table>
        <thead>
          <tr>
            <th>Store</th>
            <th>Amount</th>
            <th>Points</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          @for (receipt of receipts(); track receipt.id) {
          <tr>
            <td>{{ receipt.merchant_name }}</td>
            <td>\${{ receipt.total_amount }}</td>
            <td>
              <strong>+{{ receipt.points_earned }}</strong>
            </td>
            <td>
              <span class="badge" [class]="receipt.status">{{ receipt.status }}</span>
            </td>
          </tr>
          } @empty {
          <tr>
            <td colspan="4">No receipts found. Submit one above!</td>
          </tr>
          }
        </tbody>
      </table>
    </div>
  `,
  styles: [
    `
      .list-container {
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 8px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th,
      td {
        text-align: left;
        padding: 12px;
        border-bottom: 1px solid #eee;
      }
      .badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        text-transform: uppercase;
      }
      .pending {
        background: #fff3cd;
        color: #856404;
      }
    `,
  ],
})
export class ReceiptListComponent implements OnInit {
  private receiptService = inject(ReceiptService);

  // Directly link to the service's signal
  receipts = this.receiptService.receipts;

  ngOnInit() {
    this.receiptService.fetchReceipts();
  }
}
