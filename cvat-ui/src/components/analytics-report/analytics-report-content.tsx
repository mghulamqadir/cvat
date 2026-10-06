// Copyright (C) CVAT.ai Corporation
//
// SPDX-License-Identifier: MIT

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useSelector } from 'react-redux';
import Alert from 'antd/lib/alert';
import Button from 'antd/lib/button';
import Empty from 'antd/lib/empty';
import Spin from 'antd/lib/spin';
import Chart from 'chart.js/auto';

import config from 'config';
import { Project, Task, Job, getCore } from 'cvat-core-wrapper';
import { CombinedState } from 'reducers';
import PaidFeaturePlaceholder from 'components/paid-feature-placeholder/paid-feature-placeholder';
import { TimePeriod } from '.';

interface Props {
    resource: Project | Task | Job;
    timePeriod: TimePeriod | null;
}

const core = getCore();

function TaskAnnotationAnalytics({ task }: { task: Task }): JSX.Element {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const chartRef = useRef<Chart | null>(null);
    const [classes, setClasses] = useState<Array<{ label: string; count: number }> | null>(null);
    const [error, setError] = useState<Error | null>(null);
    const [loading, setLoading] = useState(true);

    const load = useCallback(async (): Promise<void> => {
        try {
            setLoading(true);
            setError(null);
            const analytics = await core.analytics.annotationCounts({ taskID: task.id });
            setClasses(analytics.classes);
        } catch (requestError: unknown) {
            setError(requestError instanceof Error ? requestError : new Error('Unable to load annotation analytics'));
        } finally {
            setLoading(false);
        }
    }, [task.id]);

    useEffect(() => {
        load();
    }, [load]);

    useEffect(() => {
        chartRef.current?.destroy();
        chartRef.current = null;

        if (!canvasRef.current || !classes?.length) {
            return undefined;
        }

        chartRef.current = new Chart(canvasRef.current, {
            type: 'bar',
            data: {
                labels: classes.map(({ label }) => label),
                datasets: [{
                    label: 'Shapes',
                    data: classes.map(({ count }) => count),
                    backgroundColor: '#1890ff',
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 },
                        title: { display: true, text: 'Shape count' },
                    },
                },
            },
        });

        return () => chartRef.current?.destroy();
    }, [classes]);

    if (loading) {
        return <Spin size='large' />;
    }

    if (error) {
        return (
            <Alert
                type='error'
                showIcon
                message='Could not load annotation analytics'
                description={(
                    <>
                        {error.message}
                        <Button type='link' onClick={load}>Retry</Button>
                    </>
                )}
            />
        );
    }

    if (!classes?.length) {
        return <Empty description='This task has no configured labels' />;
    }

    return <canvas ref={canvasRef} aria-label='Annotation counts by class' role='img' />;
}

function AnalyticsReportContent({ resource }: Props): JSX.Element {
    if (resource instanceof Task) {
        return <TaskAnnotationAnalytics task={resource} />;
    }

    return (
        <PaidFeaturePlaceholder featureDescription={config.PAID_PLACEHOLDER_CONFIG.features.analyticsReport} />
    );
}

function AnalyticsReportContentWrap(props: Readonly<Props>): JSX.Element {
    const overrides = useSelector(
        (state: CombinedState) => state.plugins.overridableComponents.analyticsReportPage.content,
    );

    if (overrides.length) {
        const [Component] = overrides.slice(-1);
        return <Component {...props} />;
    }

    return <AnalyticsReportContent {...props} />;
}

export default React.memo(AnalyticsReportContentWrap);
