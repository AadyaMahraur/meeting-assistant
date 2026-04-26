import ActionItemsTable from "./ActionItemsTable";
import DecisionsList from "./DecisionsList";
import BlockersList from "./BlockersList";
import EmailDraftView from "./EmailDraftView";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

const ResultView = ({ meeting }) => {
  if (!meeting) return null;

  return (
    <div className="space-y-10 animate-in fade-in duration-500">
      
      {/* 1. Executive Summary Highlight */}
      {/* FIX: Removed the rogue div line. Added border-t-4 and border-t-blue-600 directly to the Card */}
      <Card className="bg-blue-50/50 border-blue-200 border-t-4 border-t-blue-600 shadow-sm overflow-hidden">
        {/* FIX: Added generous responsive padding (p-6 md:p-8) */}
        <CardContent className="p-6 md:p-8">
          <div className="flex items-center gap-2 mb-4">
            <Badge variant="outline" className="bg-blue-100 text-blue-700 border-blue-300 uppercase tracking-tighter text-[10px]">
              AI Generated Summary
            </Badge>
          </div>
          <h3 className="text-xl font-bold text-blue-900 mb-3">Executive Summary</h3>
          <p className="text-blue-800 leading-relaxed italic text-lg text-left">
            "{meeting.short_summary}"
          </p>
        </CardContent>
      </Card>

      {/* 2. Detailed Summary Section */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold tracking-tight">Detailed Overview</h2>
        </div>
        <Separator />
        
        {/* FIX: Removed 'bg-transparent' and 'p-0'. Wrapped it in a clean white card so it matches the executive summary's margins */}
        <Card className="bg-white border-gray-200 shadow-sm overflow-hidden">
          {/* FIX: Standardized padding to match the box above */}
          <CardContent className="p-6 md:p-8">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap text-[1.05rem]">
              {meeting.detailed_summary}
            </p>
          </CardContent>
        </Card>
      </section>

      {/* 3. Core Outcomes Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        <div className="space-y-2">
          <ActionItemsTable items={meeting.action_items || []} />
        </div>
        <div className="space-y-2">
          <DecisionsList items={meeting.decisions || []} />
        </div>
      </div>

      {/* 4. Blockers and Risks */}
      <section className="space-y-4">
         <BlockersList items={meeting.blockers || []} />
      </section>

      {/* 5. Follow-up Assets */}
      <section className="pt-6">
        <EmailDraftView text={meeting.followup_email} />
      </section>
      
      <footer className="text-center pb-10 mt-8">
        <p className="text-xs text-muted-foreground">
          Meeting analyzed on {new Date(meeting.created_at).toLocaleString()}
        </p>
      </footer>
    </div>
  );
};

export default ResultView;